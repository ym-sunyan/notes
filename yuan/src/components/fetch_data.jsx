
export async function fetchData(url, options = {}) {
    // 处理请求的发送和响应的处理
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            debugger
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // 或者 response.text() 如果响应不是JSON
    } catch (error) {
        console.error("Error fetching data:", error);
        debugger
        throw error; // 重新抛出错误以便调用者处理
    }
}

// GET 请求
export async function get(url) {
    // 功能：请求从服务器检索特定资源。GET 请求应该只检索数据而不产生其他效果。
    // 请求体：通常不会在 GET 请求中包含请求体。
    // 幂等性：是，多次执行相同操作的结果与执行一次相同。
    // 安全性：是，GET 请求不应产生服务器上的副作用。
    // 缓存：响应可以被缓存。
    // 例子：获取一个网页的内容。
    return fetchData(url);
}
// // Demo 发送 GET 请求
// get("http://10.233.202.137:7878/datas")
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// GET 请求
export async function get2(url, id) {
    // 基于id获得某条数据
    // get2("http://10.233.202.137:7878/datas?id=0")
    // 功能：请求从服务器检索特定资源。GET 请求应该只检索数据而不产生其他效果。
    // 请求体：通常不会在 GET 请求中包含请求体。
    // 幂等性：是，多次执行相同操作的结果与执行一次相同。
    // 安全性：是，GET 请求不应产生服务器上的副作用。
    // 缓存：响应可以被缓存。
    // 例子：获取一个网页的内容。
    return fetchData(url);
}
// // Demo 发送 GET 请求
// get2("http://10.233.202.137:7878/datas?id=0")
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// GET 请求
export async function get_datas_from_to(url, _page, _per_page) {
    // json-server 分页方法：
    // _page=2 第二页
    // _per_page= 每页十条数据
    // url = "http://10.233.202.137:7878/datas?_page=2&_per_page=10"
    url = `${url}?_page=${_page}&_per_page=${_per_page}`

    // 其他数据库会有不同
    // 功能：请求从服务器检索特定资源。GET 请求应该只检索数据而不产生其他效果。
    // 请求体：通常不会在 GET 请求中包含请求体。
    // 幂等性：是，多次执行相同操作的结果与执行一次相同。
    // 安全性：是，GET 请求不应产生服务器上的副作用。
    // 缓存：响应可以被缓存。
    // 例子：获取一个网页的内容。
    return fetchData(url);
}
// Demo 发送 GET 请求
// get_datas_from_to("http://10.233.202.137:7878/datas", 2, 10)
//   .then(data =>{ console.log(data)
//     debugger})
//   .catch(error => {
//     console.error(error)
//     debugger
//   });

// POST 请求
export async function post(url, data={}) {
    // 功能：向服务器提交数据以创建新资源或执行某些操作（例如提交表单数据或上传文件）。
    // 请求体：通常在请求体中包含要提交的数据。
    // 幂等性：否，多次提交数据可能会导致资源创建多次。
    // 安全性：否，POST 请求可能会在服务器上产生副作用。
    // 缓存：响应通常不会被缓存。
    // 例子：提交表单、上传文件。
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    };
    return fetchData(url, options);
    fetchData(url, options).then(data=>{
        console.log(data)
        debugger
        return data
    }).catch(error=>{
        console.error(error)
        debugger
        return null
    })

}
// Demo 发送 POST 请求
// post("http://10.233.202.137:7878/datas", { key: "value" })
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// PUT 请求
export async function put(url, data) {
    // 功能：将指定资源的状态更改为请求中提供的状态。如果资源不存在，则创建它。
    // 请求体：通常在请求体中包含资源的新状态。
    // 幂等性：是，多次执行相同操作的结果与执行一次相同。
    // 安全性：否，PUT 请求可能会改变服务器上的资源。
    // 缓存：响应通常不会被缓存。
    // 例子：更新数据库记录、更新文件
    const options = {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    };
    return fetchData(url, options);
}
// Demo 发送 PUT 请求
// put("http://10.233.202.137:7878/datas/123", { key: "newValue" })
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// PATCH 请求
export async function patch(url, data) {
    // 部分更新：PATCH 仅更新资源的某些部分。它不需要提交资源的完整表示，只需要提交变化的部分。
    // 幂等性：PATCH 请求不一定是幂等的。多次应用相同的 PATCH 请求可能会产生不同的结果，这取决于资源的状态和 PATCH 操作的具体实现。
    // 安全性：PATCH 请求可能会产生服务器上的副作用，因此它不是安全的。使用 PATCH 请求时，需要确保操作的安全性。
    // 缓存：PATCH 请求的响应通常不会被缓存，因为部分更新可能会改变资源的状态，从而影响缓存的有效性。
    // 请求体：PATCH 请求通常包含一个请求体，其中包含了要应用到资源上的变化。
    // 应用场景：适用于需要更新资源的特定字段而不需要更新整个资源的情况。例如，更新用户的配置设置或修改订单的某个属性。
    const options = {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    };
    return fetchData(url, options);
}
// // Demo 发送 PATCH 请求
// patch("http://10.233.202.137:7878/datas/0", { arn: "0000" })
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// DELETE 请求
export async function del(url) {
    // 功能：删除指定的资源。
    // 请求体：通常不会在 DELETE 请求中包含请求体。
    // 幂等性：是，多次删除同一个资源的结果与删除一次相同。
    // 安全性：否，DELETE 请求可能会删除服务器上的资源。
    // 缓存：响应通常不会被缓存。
    // 例子：从服务器删除文件或数据库记录
    const options = {
        method: "DELETE"
    };
    return fetchData(url, options);
}
// Demo 发送 DELETE 请求
// del("http://10.233.202.137:7878/datas/123")
//   .then(() => console.log("Resource deleted"))
//   .catch(error => console.error(error));

// OPTIONS 请求
export async function options(url) {
    // 功能：描述目标资源的通信选项。它用于获取服务器支持的HTTP方法，常用于跨域资源共享（CORS）预检请求。
    // 请求体：通常不包含请求体。
    // 幂等性：是，OPTIONS 请求不应产生服务器上的副作用。
    // 安全性：是，OPTIONS 请求不应产生服务器上的副作用。
    // 缓存：响应可以被缓存。
    // 例子：询问服务器支持哪些HTTP方法
    const options = {
        method: "OPTIONS"
    };
    return fetchData(url, options);
}
// Demo 发送 OPTIONS 请求
// options("http://10.233.202.137:7878/datas")
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// HEAD 请求
export async function head(url) {
    // 功能：请求获取与GET请求相同的响应，但没有响应体。用于获取资源的元数据。
    // 请求体：通常不会在 HEAD 请求中包含请求体。
    // 幂等性：是，HEAD 请求不应产生服务器上的副作用。
    // 安全性：是，HEAD 请求不应产生服务器上的副作用。
    // 缓存：响应可以被缓存。
    // 例子：检查资源是否存在或获取资源的新鲜度
    const options = {
        method: "HEAD"
    };
    return fetchData(url, options);
}
// Demo 发送 HEAD 请求
// head("http://10.233.202.137:7878/datas")
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

// TRACE 请求
export async function trace(url) {
    // 功能：请求服务器回显其收到的请求信息。它主要用于诊断，以验证请求是否如预期那样被发送和接收。
    // 请求体：通常不包含请求体。
    // 幂等性：是，TRACE 请求不应产生服务器上的副作用。
    // 安全性：否，TRACE 请求可能会暴露敏感信息。
    // 缓存：响应通常不会被缓存。
    // 例子：诊断问题，检查请求是否被代理服务器修改
    const options = {
        method: "TRACE"
    };
    return fetchData(url, options);
}
// Demo 发送 TRACE 请求
// trace("http://10.233.202.137:7878/datas")
//   .then(data =>{ console.log(data)})
//   .catch(error => console.error(error));

