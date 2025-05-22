import { configureStore } from "@reduxjs/toolkit";
import { authApi } from "../../shared/api/authApi";
import { baseApi } from "../../shared/api/baseApi";

export const store = configureStore({
    reducer: {
    [authApi.reducerPath]: authApi.reducer,
    [baseApi.reducerPath]: baseApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(authApi.middleware)
      .concat(baseApi.middleware),
})