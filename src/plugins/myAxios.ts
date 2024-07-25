import axios from 'axios';

const MyAxios = axios.create({
    baseURL: 'http://110.41.66.229:5174/',
    adapter: ['fetch'],
    // timeout: 5000,
    withCredentials: 'cors',
})

MyAxios.interceptors.response.use(response => {
    response.data.status = response.status
    return response.data
}, error => {
    return Promise.reject(error)
})

export default MyAxios