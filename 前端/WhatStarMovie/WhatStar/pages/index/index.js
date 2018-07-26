//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: '测测你和哪个明星最像',
    userInfo: {},
    tmpFilePaths: '',
    starname: '',
    starpic: '',
    similarity: '',
    moviename: '',
    moviedes: '',
    loadingHidden: true,
  },
  onLoad: function () {
    var that = this
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function (userInfo) {
      that.setData({
        userInfo: userInfo
      })
    })
  },

  // 上传图片
  upload: function () {
    var that = this
    wx.chooseImage({
      count: 1, // 默认9  
      sizeType: ['compressed'], // 可以指定是原图还是压缩图，默认二者都有  
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有 
      success: function (res) {
        //返回选定照片的本地文件路径列表
        var tempFilePaths = res.tempFilePaths
        //打开 loading 动画
        that.setData({
          loadingHidden: false,
          tempFilePaths: tempFilePaths[0]
        });
        wx.uploadFile({
          header: { 'content-type': 'application/json' },
          url: '.../starmovie/',
          filePath: tempFilePaths[0], // 待上传图片的地址
          name: 'upfile',
          formData: {
            'user': that.data.userInfo.nickName,
          },
          success: function (res) {
            // 关闭 loading 动画
            console.log(res)
            that.setData({
              loadingHidden: true,
            });
            var ret = JSON.parse(res.data)//字符串转对象，服务器返回的数据
            console.log(ret)
            if (ret.errorCode == 1){
              wx.showToast({
                title: '图片上传成功',
                icon: 'success',
                duration: 2000,
              });
              var starpic = ret.starpic.slice(1)
              that.setData({
                tmpFilePaths: tempFilePaths,
                starname: ret.starname,
                starpic: starpic,
                similarity: ret.similarity,
                moviedes: ret.moviedes, 
                moviename: ret.moviename             
              });
              console.log(starpic)
              //页面跳转传递参数
              wx.navigateTo({
                url: '../logs/logs?tmpFilePaths=' + that.data.tmpFilePaths + '&starname=' + that.data.starname + '&starpic=' + that.data.starpic + '&similarity=' + that.data.similarity + '&moviedes=' + that.data.moviedes + '&moviename=' + that.data.moviename
              })
            }
            else if(ret.errorCode == 0 ){
              var hint = ' 检测到多张人脸，请换一张照片'
              wx.showToast({
                title: hint,
                icon: 'none',
                duration: 3000,
              });
            }
            else if(ret.errorCode == -1){
              var hint = '没有检测到人脸，请换一张照片'
              wx.showToast({
                title: hint,
                icon: 'none',
                duration: 3000,
              });
            }
            else{
              var hint = '图片上传失败'
              wx.showToast({
                title: hint,
                icon: 'none',
                duration: 3000,
              });
            }
          },
          fail: function (res) {
            console.log(res)
            // 关闭 loading 动画
            that.setData({
              loadingHidden: true
            });
            wx.showToast({
              title: '图片上传失败',
              icon: 'loading',
              duration: 1500,
            })
          }
        })
      }
    }) 
  }
})