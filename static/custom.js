var _hmt = _hmt || [];
(function () {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4d63ba711285f7c696d0505f5e30ba96";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();

// 通知栏关闭功能
function closeNotice() {
  var noticeBar = document.getElementById("notice-bar");
  if (noticeBar) {
    noticeBar.classList.add("hidden");
  }
}

// 30秒后自动关闭通知栏
window.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    closeNotice();
  }, 30000); // 30秒 = 30000毫秒

  // 随机文章功能 - 从所有文章中随机选择
  var randomLink = document.querySelector(".menu-action-random");
  if (randomLink) {
    randomLink.addEventListener("click", function (e) {
      e.preventDefault();

      // 显示加载提示
      var originalContent = randomLink.innerHTML;
      randomLink.style.opacity = "0.5";
      randomLink.innerHTML =
        '<i class="fa fa-spinner fa-spin" aria-hidden="true"></i> 加载中...';

      // 从后端 API 获取随机文章
      fetch("/api/random-article")
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.error) {
            alert("获取随机文章失败：" + data.error);
            return;
          }

          if (data.link) {
            // 在新标签页打开随机文章
            window.open(data.link, "_blank");
          } else {
            alert("无法获取文章链接");
          }
        })
        .catch(function (error) {
          console.error("获取随机文章失败:", error);
          alert("获取随机文章失败，请稍后重试");
        })
        .finally(function () {
          // 恢复按钮状态
          randomLink.style.opacity = "1";
          randomLink.innerHTML = originalContent;
        });
    });
  }
});
