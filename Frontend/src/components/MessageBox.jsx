import { useState, useRef, useEffect } from "react";
import { useDispatch } from 'react-redux'
import { setForm, updateField, patchForm, resetForm } from '../redux/slices/formContext.js'

const BotIcon = () => (
  <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
      <path d="M12 2a2 2 0 012 2v1h3a2 2 0 012 2v2h1a1 1 0 010 2h-1v5a2 2 0 01-2 2H7a2 2 0 01-2-2V9H4a1 1 0 010-2h1V7a2 2 0 012-2h3V4a2 2 0 012-2zm0 7a1 1 0 100 2 1 1 0 000-2zm-3 4a1 1 0 100 2 1 1 0 000-2zm6 0a1 1 0 100 2 1 1 0 000-2z" />
    </svg>
  </div>
);

const UserIcon = () => (
  <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center shrink-0">
    <svg className="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
      <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
    </svg>
  </div>
);

export default function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  // remove inputHeight state; control height via textarea DOM
  // kept a placeholder state to avoid reordering hooks in case other code relies on hook order
  const [__placeholderUnused, __setPlaceholderUnused] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);
  const dispatch = useDispatch()

  // Initialize textarea height on mount
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '40px';
    }
  }, []);

  useEffect( () => {
    const chats = sessionStorage.getItem('chatHistory');
    if (chats){
      const parsed = JSON.parse(chats)
      setMessages(parsed)
    }
  }, [] )

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const  sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = {role: "user", content: trimmed };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput("");
    // reset textarea height to default after sending
    if (textareaRef.current) textareaRef.current.style.height = '40px';
    try{
      console.log(`sending data ${updatedMessages}`)
      const res = await fetch(`http://127.0.0.1:8000/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"messages": updatedMessages})
      })

      const data = await res.json()
      const response = data.data
      const reply = {role: "assistant", content: response.content }
      const finalMessages = [...updatedMessages, reply]
      setMessages(finalMessages)
      sessionStorage.setItem('chatHistory', JSON.stringify(finalMessages))
    }catch (error){
      alert(error)
    }


  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const refreshChat = () => {
    sessionStorage.removeItem('chatHistory')
    setMessages([])
  }

  const handleInputChange = (e) => {
    setInput(e.target.value);
    // Auto-expand textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // Reset height to calculate new height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set height to scrollHeight
    }
  }

  // Recalculate height when `input` changes (covers programmatic updates/pastes)
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  return (
    <div className="h-[92vh]">
      <div className="flex flex-col w-full h-[100%] bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200">
          <div>
            <p className="text-black font-semibold text-sm">AI Assistant</p>
            <p className="text-indigo-600 text-xs">Log interactions via chat</p>
          </div>
          <button onClick={refreshChat} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold text-sm transition-colors">New Chat</button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 bg-gray-50">
          {messages?.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-end gap-2 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
            >
              {msg.role === "assistant" ? <BotIcon /> : <UserIcon />}

              <div
                className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-indigo-600 text-white rounded-br-sm"
                    : "bg-white text-gray-800 rounded-bl-sm shadow-sm border border-gray-100"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="flex flex-col-reverse items-end gap-2 px-4 py-3 border-t border-gray-200 bg-white">
          <div className="relative w-full">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Type a message..."
              rows={1}
              style={{ overflow: 'hidden' }}
              className="w-full pr-12 px-4 py-2 text-sm bg-gray-100 rounded-lg outline-none focus:ring-2 focus:ring-indigo-400 transition resize-none min-h-[40px]"
            />

            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              aria-label="Send message"
              className="absolute right-2 bottom-2 w-9 h-9 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 rounded-full flex items-center justify-center transition"
            >
              <svg className="w-4 h-4 text-white rotate-90" fill="currentColor" viewBox="0 0 24 24">
                <path d="M2 21l21-9L2 3v7l15 2-15 2v7z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}