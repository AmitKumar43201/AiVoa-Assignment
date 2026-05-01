import { configureStore } from '@reduxjs/toolkit'
import formInfoReducer from './slices/formContext.js'
import queryResultsReducer from './slices/queryResultsSlice.js'

export const store = configureStore({
  reducer: {
    form: formInfoReducer,
    queryResults: queryResultsReducer
  },
})

console.log(store)