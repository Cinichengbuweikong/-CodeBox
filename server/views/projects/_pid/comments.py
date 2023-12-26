from typing import List, Optional
from datetime import datetime

from fastapi import Query, Path, Body, Depends

from . import router
from models.ProjectComments import ProjectComments
from models.commentLike import CommentLike
from models.Users import Users
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.comments.getProjectCommentsResponseSchema import GetProjectCommentsResponseSchema
from constants import ResopnseOperationResultType
from depends.userInfoDependence import userInfo


@router.get("/comments")
async def getProjectComments(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    page: Optional[int] = Query(default=1, gt=0)
):
    """
    获取 pid 指定的项目的评论
    """

    perpage = 6
    """
    每页有多少评论
    """

    allComments: List[ProjectComments] = await ProjectComments.filter(pid=pid).all()

    comments: List[GetProjectCommentsResponseSchema] = []

    for c in allComments[(page-1)*perpage: page*perpage]:  # type: ignore
        youlike = False

        if user != None:
            # 先找到所有当前用户的评论 再从这些评论中找出当前评论 id 的评论
            targetLike: CommentLike | None = \
                await CommentLike.filter(uid=user.uid).filter(cid=c.cid).first()

            if targetLike != None:
                youlike = targetLike.like
        
        comments.append(GetProjectCommentsResponseSchema(
            cid=c.cid,
            uid=c.uid,
            comment=c.comment,
            date=c.date,
            like=c.like,
            youlike=youlike,
        ))

    return {
        "total": len(comments),
        "perpage": perpage,
        "page": page,
        "data": comments
    }


@router.post("/comments")
async def newComment(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    comment: str = Body(embed=True)
):
    """
    新建一条评论
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )

    newProjectComment = ProjectComments(
        pid=pid,
        uid=user.uid,
        comment=comment,
        date=datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    )

    await newProjectComment.save()

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.put("/comments")
async def modifyComment(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    cid: int = Body(embed=True),
    comment: str = Body(embed=True),
):
    """
    修改评论
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    

    targetProjectComments: ProjectComments | None = \
        await ProjectComments.filter(cid=cid).first()

    if targetProjectComments == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="comment not found"
        )
    

    userTargetProjecrComments: ProjectComments | None = \
        await targetProjectComments.filter(uid=user.uid).first()

    if userTargetProjecrComments == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this comments is not yours"
        )
    

    targetProjectComments.comment = comment

    await targetProjectComments.save()


    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.patch("/comments")
async def likeOrDislikeComments(
    user: Users | None = Depends(userInfo),
    cid: int = Body(embed=True),
    like: bool = Body(embed=True),
):
    """
    赞或踩一条评论
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    

    # 修改 commentLike 对象
    targetLike: CommentLike | None = \
        await CommentLike.filter(uid=user.uid).filter(cid=cid).first()

    if targetLike == None:
        targetLike = CommentLike(
            uid=user.uid,
            cid=cid,
            like=True if like else False
        )
    else:
        targetLike.like = like
    
    await targetLike.save()


    # 修改评论中的赞数
    targetComment: ProjectComments | None = \
        await ProjectComments.filter(cid=cid).first()
    
    if targetComment == None:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="comment not found"
        )
    
    if like == True:
        targetComment.like = targetComment.like + 1
    else:
        targetComment.like = targetComment.like - 1

    await targetComment.save()


    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.delete("/comments")
async def deleteComment(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    cid: int = Body(embed=True),
):
    """
    删除评论
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    

    targetProjectComments: ProjectComments | None = \
        await ProjectComments.filter(cid=cid).first()

    if targetProjectComments == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="comment not found"
        )
    

    userTargetProjecrComments: ProjectComments | None = \
        await targetProjectComments.filter(uid=user.uid).first()

    if userTargetProjecrComments == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this comments is not yours"
        )
    

    await targetProjectComments.delete()


    allCommentLikes: List[CommentLike] | None = \
        await CommentLike.filter(cid=cid).all()
    
    for l in allCommentLikes:
        await l.delete()


    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
