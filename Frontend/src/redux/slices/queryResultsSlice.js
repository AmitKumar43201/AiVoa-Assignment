import { createSlice } from '@reduxjs/toolkit'

const queryResultsSlice = createSlice({
    name: 'queryResults',
    initialState: { results: [] },
    reducers: {
        setQueryResults: (state, action) => {
            state.results = action.payload
        },
        deleteHcp: (state, action) => {
            const hcpName = action.payload;
            state.results = state.results.filter((item) => item.hcp_name !== hcpName)
        },
        clearQueryResults: (state) => {
            state.results = []
        }
    }
})

export const { setQueryResults, clearQueryResults, deleteHcp } = queryResultsSlice.actions
export default queryResultsSlice.reducer