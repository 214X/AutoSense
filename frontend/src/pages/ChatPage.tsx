import React, { useState } from "react";
// Component imports
import AssistantMessageBox from "../components/AssistantMessageBox";
import UserMessageBox from "../components/UserMessageBox";
import ChatInputArea from "../components/ChatInputArea";
import ChatHeader from "../components/ChatHeader";
// Type imports
import type { ChatMessage } from "../types/ChatMessage";

const exampleMessages = [
    <AssistantMessageBox content= "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Placeat amet dolor dolores sequi a unde aliquid laborum eligendi beatae! Molestias minus nisi amet, impedit, fuga vero quasi maxime, architecto sapiente esse numquam magnam laborum tenetur similique explicabo dolores. Dolorem odio rem eum nesciunt explicabo eveniet!"/>,
    <UserMessageBox content="Lorem ipsum dolor sit amet consectetur adipisicing elit. Possimus maiores magni, placeat sed architecto suscipit expedita? Aliquid inventore totam eius?" />,
]


const ChatPage: React.FC = () => {
    const [inputValue, setInputValue] = useState("")

    const handleSend = () => {
        const trimmed = inputValue.trim();
        if (!trimmed) return;

        const userMessage: ChatMessage = {
            role: "user",
            message: trimmed,
            timestamp: new Date().toISOString(),
        };

        console.log(userMessage.message);

        setInputValue("");
    }

    return (
        <div className="chat-page">
            {/* Header */}
            <ChatHeader />
            {/* Messages */}
            <div className="chat-messages">
                <div className="chat-messages">
                    {exampleMessages.map((message, index) => (
                        <React.Fragment key={index}>
                            {message}
                        </React.Fragment>
                    ))}
                </div>
            </div>
            {/* UserInputArea */}
            <ChatInputArea 
                value={inputValue} 
                onChange={setInputValue} 
                onSend={handleSend}  />
        </div>
    )
}


export default ChatPage;