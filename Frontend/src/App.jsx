import { useState , useEffect} from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { setForm, patchForm } from './redux/slices/formContext.js'
import { Route, Routes, useNavigate } from "react-router-dom";
import MainPage from './pages/MainPage.jsx'
import QueryResultsTable from './pages/Table.jsx'
import {setQueryResults} from './redux/slices/queryResultsSlice.js'


function App() {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const handleEvent = (type, data) => {
    if (type === 'createform'){
        dispatch(setForm(data))
    }
    if (type === 'openForm'){
        dispatch(setForm(data))
    }
    if (type === 'editform'){
        dispatch(patchForm(data))
    }
    if (type === 'suggestFollowUps'){
        dispatch(patchForm(data))
    } 
    if (type === 'queryResult'){
        dispatch(setQueryResults(data))
        navigate('/table')
    }   
  }
  useEffect(() => {
      const socket = new WebSocket("ws://127.0.0.1:8000/ws");
      socket.onopen = () => {
          console.log("Connected to backend socket");
      };

      socket.onclose = () => {
          console.log("Disconnected from backend socket");
      };

      socket.onerror = (error) => {
          console.error("Socket error:", error);
      };

      socket.onmessage = (event) => {
      const { event: type, data } = JSON.parse(event.data);
      handleEvent(type,data)
      console.log(type)
      console.log(data)
      };

      return () => {
          socket.close();   // cleanup on component unmount
      };
  }, []);

  const home = () => {navigate('/')}
  const table = () => {navigate('/table')}

  return (
    <>
    <div className='flex flex-col h-[100%]'>
      <div className='flex flex-row items-center justify-center gap-4 py-4 bg-white border-b border-gray-200'>
        <button onClick={home} className='px-6 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg font-semibold transition-colors'>Home</button>
        <button onClick={table} className='px-6 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg font-semibold transition-colors'>Table</button>
      </div>
      <div className='flex-1'>
        <Routes>
            <Route path='/' element={<MainPage/>} />
            <Route path='/table' element= {<QueryResultsTable/>}  />
        </Routes>
      </div>
    </div>
    </>
  )
}

export default App
