import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query";

const URL = "/api/auth/jwt";

interface UserPayload {
    username: string,
    password: string,
}

interface Response {
     token: string,
     userId: number,
}

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({ baseUrl: URL }),
  endpoints: (build) => ({
    login: build.mutation<Response, UserPayload>({
      query: (body) => (
        { 
            url: 'login', 
            method: 'POST', 
            body 
        }
      ),
    }),
    refresh: build.mutation<Response, { refreshToken: string }>({
        query: (body) => (
            {
                url: "refresh",
                method: "POST",
                body,
            }
        )
    }),
    verify: build.mutation<Response, UserPayload>({
        query: (body) => (
            {
                url: "verify",
                method: "POST",
                body,
            }
        )
    })
  }),
});