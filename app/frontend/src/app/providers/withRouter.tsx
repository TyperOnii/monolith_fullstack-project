import { RouterProvider } from 'react-router-dom'
import { router } from '../../shared/model/router/router'

export const WithRouter = () => {
  return (
    <RouterProvider router={router}/>
  )
}
