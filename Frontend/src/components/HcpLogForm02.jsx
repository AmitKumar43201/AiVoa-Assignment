import React, {useState, useEffect} from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Form from './Form';
import { setForm, updateField, patchForm, resetForm } from '../redux/slices/formContext.js'
import {deleteHcp} from '../redux/slices/queryResultsSlice.js'

function HcpLogForm02() {


  const form = useSelector((state) => state.form)
  const dispatch = useDispatch()

  const set = (key) => (val) => {
    dispatch(updateField({
      key,
      value: val
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave?.(form);
  };

  const onSave = async (data) => {
    console.log("Saved:", data)
    console.log(form)
    try{
      const res = await fetch(`http://127.0.0.1:8000/save-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      const response = await res.json()
      alert(response.message)
    }catch (error){
      alert(error)
    }
}
  const onReset = () => dispatch(resetForm())
  const onDelete = async () => {
    try{
      const res = await fetch(`http://127.0.0.1:8000/delete-data/${form.hcp_name}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      if (res.ok){
      const data = await res.json()
      alert(data.message)
      dispatch(resetForm())
      const hcp_name = form.hcp_name
      dispatch(deleteHcp(hcp_name))
      }

    }catch (error){
      alert(error)
    }  
  }

  return (
    <Form form={form}  set={set} handleSubmit={handleSubmit} onSave={onSave} onReset={onReset} onDelete={onDelete}/>
  )
}

export default HcpLogForm02
