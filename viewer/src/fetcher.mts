import { ofetch } from "ofetch"

export const fetcher = ofetch.create({
  baseURL: "http://localhost:2024",
})

