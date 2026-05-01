import React from 'react'
import HcpLogForm02 from '../components/HcpLogForm02.jsx'
import Chatbox from '../components/MessageBox.jsx'

function MainPage() {
  return (
    <div className='grid grid-cols-[3fr_2fr] h-[100%]'>
        <HcpLogForm02/>
        <Chatbox/>
    </div> 
  )
}

export default MainPage
