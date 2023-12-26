# API

本文件是后端需要向前端提供的 API 接口的文档  使用 RESTful 风格设计

这里所示的 api 均需添加 /api 前缀  例如 /api/signup





## 前台

/sendVerifyCode

- POST

  - 向用户发送验证码

    - 请求

      ```typescript
      {
          email: String,  // 用户的邮箱
          uid?: String,  // 用户的 uid
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
          verifyCode: string,  // 验证码
      }
      ```



/signup

- POST

  - 用户注册

    - 提供

      ```typescript
      {
          username: String,  // 用户名
          email: String,  // 用户的邮箱
          password: String,  // 用户的密码
          verifyCode: String  // 验证码
      }
      ```
  
- 返回
  
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/login

- POST

  - 用户登录

    - 提供

      ```typescript
      {
          email: String,  // 用户的邮箱
          password: String,  // 用户的密码
          verifyCode: String  // 验证码
      }
      ```

    - 返回

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
          
      // 注: 响应不在响应体中返回任何用户信息 但需要在 cookie 中设置 jwt
      // 同时 jwt 必须设置 httpOnly 和 sameSite 等安全属性
      ```



/logout

- POST

  - 用户退出登录

    - 提供

      ```typescript
      // 无
      ```

    - 响应

      ```typescript
      // 无 只需要在响应中设置删除 cookie 即可
      ```



/user

- GET

  - 获取用户的信息

    - 请求

      ```typescript
      // 不需要请求体 但需要携带 cookie
      // 可选携带 uid=? 查询参数 携带的话就是查询指定 uid 用户的信息
      ```
  ```
  
  ```
  
- 响应
  
      ```typescript
      {
          uid: String,  // 当前登录用户的 uid
          username: String,  // 用户名
          avatarurl: String,  // 用户头像地址
          coin: Number,  // 用户的硬币数
          description: String,  // 用户自我介绍
          email: string,  // 用户的邮箱
      }
      ```
  
- POST

  - 修改用户信息

    - 请求

      ```typescript
      {  // FormData
          username?: String,  // 用户名
          password?: String,  // 用户密码 需要验证码
          avatarimg?: File,  // 用户头像
          description?: String,  // 用户自我介绍
          code?: String,  // 如果是修改密码的话 则需要修改验证码
    }
      ```

    - 响应
    
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

- DELETE

  - 注销用户

    - 请求

      ```typescript
      {
          verifyCode: String,  // 验证码
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/user/projects

- GET

  - 获取指定 uid 用户所有上传的项目的信息

    - 请求

      ```typescript
      // 需携带 uid=? 参数 就是获取指定 uid 用户的所有上传的项目
      ```

    - 响应

      ```typescript
      Array<{
          pid: Number,  // 项目 id
          projectname: String,  // 项目名
          description: String,  // 项目介绍
          effectimg: string  // 效果图
      }>
      ```

- POST

  - 修改当前登录用户指定 id 对应的项目的信息

    - 请求

      ```typescript
    // 需要提供如下 formData  需携带 cookie
      pid: Number,  // 要修改的项目的 id
      projectname?: String,  // 项目名
      description?: String,  // 项目介绍
      effectimg?: string  // 效果图
      ```

  - 响应

    ```typescript
    {
        code: Number,  // 响应状态码
        result: String,  // "ok" | "fail"  操作是否成功
        reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
    }
    ```

    

- PATCH

  - 当前登录用户新建一个项目

    - 请求

      ```typescript
      // 需携带 cookie
      {
          projectname: String,  // 项目名
      }
      ```
    
    - 返回
    
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
          pid: Number,  // 新建的项目的 id
      }
      ```
    
      
  
- DELETE

  - 删除当前登录用户项目中指定 id 对应的项目

    - 请求

      ```typescript
      // 需携带 cookie
      {
        pid: str,  // 要修改的项目的 id
      }
      ```
  ```
    
    - 响应
    
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
  ```



/user/stars

- GET

  - 获取指定 uid 用户收藏的项目

    - 请求

      ```typescript
      // 不需要请求体 但需要携带 cookie
      ```

    - 响应

      ```typescript
      Array<{
          pid: String,  // 项目 id
          uid: String,  // 该项目所属用户的 uid
          projectname: String,  // 项目名
          description: String,  // 项目介绍
          effectimg: string  // 效果图
      }>
      ```

- POST

  - 新建收藏
    一般来说用户只允许在自己的收藏中添加收藏 因此在服务端我们需要判断当前 pid 对应的项目是否存在于当前 uid 对应的用户的项目中

    - 请求

      ```typescript
      {
          pid: Number,  // 要收藏的项目的项目 id
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

      

- DELETE

  - 删除收藏
    一般来说用户只允许在自己的收藏中删除收藏 因此在服务端我们需要判断当前 pid 对应的项目是否存在于当前 uid 对应的用户的项目中

    - 请求

      ```typescript
      {
          pid: Number,  // 要被删除的收藏的项目的项目 id
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/stars

- GET

  - 查询某个项目是否被当前用户收藏了

    - 请求

      ```typescript
      // 需要携带 cookie
      // 需携带如下查询参数:
      // pid=?  项目 pid
      ```

    - 响应

      ```typescript
      {
          star: boolean,  // 该项目是否被当前用户收藏了
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/projects

- GET

  - 根据关键词搜索项目

    - 请求

      ```typescript
      // 没有请求体 通过查询参数 q=? 传递搜索关键词  page=? 获取第几页的项目
      ```

    - 响应

      ```typescript
      {
          total: Number,  // 总共有几条数据
          perpage: Number,  // 一页有几条数据
          page: Number,  // 当前是第几页
          data: Array<{
              pid: String,  // 项目 id
              uid: String,  // 该项目所属用户的 uid
              projectname: String,  // 项目名
              description: String,  // 项目介绍
              effectimg: string  // 效果图
          }>
      }
      ```



/projects/:pid/

- GET

  - 获取指定 id 对应的项目的信息

    - 请求

      ```typescript
      // 无
      ```

    - 响应

      ```typescript
      {
          pid: String,  // 项目 id
          uid: String,  // 该项目所属用户的 uid
          projectname: String,  // 项目名
          description: String,  // 项目介绍
          effectimg: string  // 效果图
      }
      ```



/projects/:pid/code

- GET

  - 获取指定 pid 项目下的所有代码文件的信息

    - 请求

      ```typescript
      // 携带如下 query 参数:
      // temp=Boolean,  // 该 pid 是否是 tpid  如果是的话则需要从 TempProjects 和 TempCodes 中获取数据
      ```
  ```
      
  - 响应
    
      ```typescript
      {
          "cid": {  // key 是代码文件的 id
              name: String,  // 代码文件名
              type: "vue" | "js",  // 代码文件类型
          }
      }
  ```
  
- POST

  - 新建代码文件
  一般来说用户只允许在自己的项目中添加文件 因此在服务端我们需要判断当前 pid 对应的项目是否存在于当前用户的项目中
    - 请求
  
      ```typescript
      {
          name: String,  // 文件名
          type: "vue" | "js",  // 文件类型
          temp?: Boolean,  // 该 pid 是否是临时工程的 pid  是的话则在此临时工程中新建文件
      }
      ```
  	
    - 响应
    
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/projects/:pid/code/:cid

- GET

  - 获取一个项目下指定代码文件的内容

    - 请求

      ```typescript
      // 携带如下 query 参数:
      // temp=Boolean,  // 该 pid 是否是 tpid  如果是的话则需要从 TempProjects 和 TempCodes 中获取数据
      // 当 temp=true 的时候需要携带 cookie
      ```
    
    - 响应
    
      ```typescript
      {
          cid: Number,  // 代码文件的 id
          pid: Number,  // 该代码文件所属的项目的 id
          name: String,  // 代码文件的名字
          type: "vue" | "js",  // 
          content: String  // 代码文件的内容
      }
      ```
  
- PATCH

  - 修改代码文件中的内容
一般来说用户只允许在自己的项目中修改文件 因此在服务端我们需要判断当前 pid 对应的项目是否存在于用户的项目中
  
- 请求
  
      ```typescript
      {
          content: String,  // 新代码内容
          temp: Boolean?,  // 该 pid 是否是 tpid  如果是的话则需要从 TempProjects 和 TempCodes 中获取数据
      }
      ```
  
  - 响应
  
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```
  
- DELETE

  - 删除代码文件
    一般来说用户只允许在自己的项目中删除文件 因此在服务端我们需要判断当前 pid 对应的项目是否存在于当前用户的项目中

    - 请求

      ```typescript
      // 需要携带 cookie
      {
      temp: Boolean?,  // 该 pid 是否是 tpid  如果是的话则需要从 TempProjects 和 TempCodes 中获取数据
      }
      ```
    
    - 响应
    
      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```



/projects/:pid/comments

- GET

  - 获取指定 pid 项目的评论

    - 请求

      ```typescript
      // 没有请求体 但需要传递如下查询参数
      // page: int,  // 获取第几页的评论
      ```
      
    - 响应
    
  ```typescript
      {
          total: Number,  // 总共有几条数据
          perpage: Number,  // 一页有几条数据
          page: Number,  // 当前是第几页
          data: Array<{
              cid: Number,  // 评论 id
              uid: Number,  // 评论用户 id
              comment: String,  // 评论
              date: String,  // 用户评论日期
              like: Number,  // 赞数
              youlike: Boolean  // 你赞成这个评论吗?
          }>
      }
  ```
  
- POST

  - 新建指定 pid 项目的评论

    - 请求

      ```typescript
      {
          comment: String,  // 评论
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

- PUT

  - 修改评论 用户只能修改自己的评论

    - 请求

      ```typescript
      {
          cid: Number,  // 评论 id
          comment: String,  // 修改后的评论
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

- PATCH

  - 修改评论 但只是点赞或点踩 每个用户只能点赞或是取消赞

    - 请求

      ```typescript
      {
          cid: Number,  // 评论 id
          like: Boolean,  // 赞?  True 就是赞  False 就是不赞
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

- DELETE

  - 删除评论
用户只能删除自己的评论
  
    - 请求

          ```typescript
          {
              cid: Number,  // 要删除的评论 id
          }
          ```

    - 响应

          ```typescript
          {
              code: Number,  // 响应状态码
              result: String,  // "ok" | "fail"  操作是否成功
              reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
          }
          ```



/projects/temporaryproject

注: 用户可以通过 /projects/:pid/code 和 /projects/:pid/code/:cid 来操作临时工程中的代码

- GET

  - 获取到一个用户的所有临时项目的信息

    - 请求

      ```typescript
      // 无 需要用户登录 登录后只能查看自己的临时项目
      // 可以传递如下查询参数: tpid: int?
    // 不传递的话则是获取当前用户的所有临时工程
      ```

    - 响应
    
      ```typescript
      Array<{
          tipd: Number,  // 本项目的临时项目 id
          uid: Number,  // 此项目的用户 id
          spid: Number?,  // 源项目 id
          name: String  // 项目名
      }> 
      ```
      

- POST

  - 创建临时项目 一般来说这样的项目就算是临时项目:
    用户在线编辑 同时还没点 "发布项目" 的项目
    用户正浏览其他人做的项目时所创建的项目 此时用户需要在线编辑代码并看到效果 同时不能影响到项目原作者的代码
    用户修改自己项目的代码时

    - 请求

      ```typescript
      {
          pid?: Number,  // 如果传递了此属性的话 则此属性是要使用的源项目的项目 id
      }
      ```
  
    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          tpid: Number,  // 创建的临时项目的项目 id
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```
  
- PUT
  
  - 将临时项目保存为自己的正式项目

    - 请求

      ```typescript
      {
        tpid: Number,  // 临时项目 id
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          pid: Number,  // 创建的项目的 id
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```

- DELETE

  - 删除临时项目

    - 请求

      ```typescript
      {
          tpid: Number,  // 要被删除的临时项目的 id
      }
      ```

    - 响应

      ```typescript
      {
          code: Number,  // 响应状态码
          result: String,  // "ok" | "fail"  操作是否成功
          reason: String,  // 如果操作失败的话 则这里是原因 否则是一个空字符串
      }
      ```





































