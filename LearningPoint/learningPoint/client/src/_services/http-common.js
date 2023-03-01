import axios from "axios";

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'XSRF-TOKEN';
axios.defaults.withCredentials = true;

export default axios.create({
  baseURL: "http://localhost:8000",
});