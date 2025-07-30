function atobUrl(url, secret) {
  try {
    return btoa(url) === secret ? '' : url;
  } catch (e) {
    return url;
  }
}

// 环境变量配置对象
const ENV_VARS = {
  KB_API: '__KB_API__',
  AI_API: '__AI_API__'
};

// 将环境变量挂载到 window 对象
Object.keys(ENV_VARS).forEach(key => {
  const secret = btoa(ENV_VARS[key]);
  window[`__${key}_VAR__`] = atobUrl(ENV_VARS[key], secret);
});

// 这里的注释不能删除，用来当做占位符！--------------------------------------
