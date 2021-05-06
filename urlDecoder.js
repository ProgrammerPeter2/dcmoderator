function decode(url, params) {
    let dataurl = req.url.split('/login?')[1]
    let datas = dataurl.split('&')
    let username = datas[0].split('=')[1]
    let password = datas[1].split('=')[1]
}