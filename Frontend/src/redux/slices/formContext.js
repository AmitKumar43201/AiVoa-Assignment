import { createSlice } from '@reduxjs/toolkit'

const initialFormState = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: new Date().toISOString().split("T")[0],
  time: new Date().toTimeString().slice(0, 5),
  attendees: [],
  topics: [],
  materials: [],
  samples: [],
  sentiment: "neutral",
  outcomes: "",
  followUps: [],
}

export const formInfoSlice = createSlice({
  name: 'formInfo',
  initialState: initialFormState,
  reducers: {

    // initial foem fill
    setForm: (state, action) => {
      return { ...state, ...action.payload }
    },

    //Single field update (manual typing)
    updateField: (state, action) => {
      const { key, value } = action.payload
      state[key] = value
    },

    //partial update (edits existing form)
    patchForm: (state, action) => {
      const payload = action.payload

      Object.keys(payload).forEach((key) => {
        const value = payload[key]

        //Handle arrays
        if (Array.isArray(state[key])) {
          if (typeof value === 'object' && !Array.isArray(value)) {
            // structured operation
            const { add = [], remove = [], replace } = value

            if (replace) {
              state[key] = replace
            } else {
              // remove items
              state[key] = state[key].filter(
                (item) => !remove.includes(item)
              )

              // add items 
              state[key] = [...state[key], ...add]
            }
          } else {
            state[key] = value
          }
        }

        else {
          state[key] = value
        }
      })
    },

    //4. Reset
    resetForm: () => initialFormState
  }
})

export const {
  setForm,
  updateField,
  patchForm,
  resetForm
} = formInfoSlice.actions

export default formInfoSlice.reducer