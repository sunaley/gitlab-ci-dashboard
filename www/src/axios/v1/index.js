import axios from '../index.js'

axios.defaults.baseURL = import.meta.env.VITE_SERVER_HOST + 'api/v1'
export default axios
