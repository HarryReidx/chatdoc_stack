import axios, { AxiosResponse } from 'axios';

axios.defaults.timeout = 1000 * 60 * 2; // 改为2分钟超时
const setInterceptors = (request) => {
  request.interceptors.response.use((res: AxiosResponse) => {
    if (
      res.headers['content-type']?.includes('application/json') &&
      (!res.config.responseType || res.config.responseType === 'json')
    ) {
      return res.data;
    } else {
      return res;
    }
  }, (error) => {
    // 错误处理
    if (error.response && error.response.data) {
      // 如果响应中有数据，直接返回错误响应数据
      return Promise.reject(error.response.data);
    }
    return Promise.reject(error);
  });
};

export const backendRequest = axios.create();
backendRequest.defaults.baseURL = process.env.BACKEND_URL;
setInterceptors(backendRequest);

export const fetch = axios.create();
setInterceptors(fetch);