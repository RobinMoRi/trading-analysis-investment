import axios from "axios";

//TODO: Fix env baseURL
export const client = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    post: {
      Accept: "application/json",
    },
    get: {
      Accept: "application/json",
    },
  },
});
