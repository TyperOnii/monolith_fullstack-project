import React, { type ReactNode } from 'react'
import { store } from '../store/store'
import { Provider } from 'react-redux'

export const WithRedux = ({children}: {children: ReactNode}) => {
  return (
     <Provider store={store}>
        {children}
    </Provider>
  )
}
