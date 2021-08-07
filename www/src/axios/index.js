import axios from 'axios'

const defaultAxios = axios.create()

defaultAxios.defaults.headers.get['Accept'] = 'application/json'
defaultAxios.defaults.headers.post['Content-Type'] = 'application/json'
export default defaultAxios
