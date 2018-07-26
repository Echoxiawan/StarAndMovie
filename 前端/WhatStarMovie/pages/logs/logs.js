//logs.js
var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    tmpFilePaths: '',
    starname: '',
    starpic: '',
    similarity: '',
    moviename: '',
    moviedes: '',
  },
  onLoad: function (options) {
    var that = this
    that.setData({
      tmpFilePaths: options.tmpFilePaths,
      starname: options.starname,
      starpic: options.starpic,
      similarity: options.similarity,
      moviedes: options.moviedes,
      moviename: options.moviename
    })
  }
})
