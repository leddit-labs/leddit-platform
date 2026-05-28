import axios from "axios"
import { BASE_API_GATEWAY } from "./endpoints"

const api = axios.create({
	baseURL: BASE_API_GATEWAY,
	//withCredentials: false, //might want this?
})

// attach JWT automatically - might be smart. Wenmin?
api.interceptors.request.use((config) => {
	const token = localStorage.getItem("access_token")

	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}

	return config
})


export default api