import { createBrowserRouter, Outlet } from "react-router-dom";
import { HomePage } from "../../../pages/public/HomePage/HomePage";
import { LoginPage } from "../../../pages/public/LoginPage/LoginPage";



export const router = createBrowserRouter([
    {
        path: "/",
        element: <Outlet/>,
        children: [
            {
                path: "/",
                element: <HomePage/>
            },
            {
                path: "/login",
                element: <LoginPage/>
            }
        ]
    }
])