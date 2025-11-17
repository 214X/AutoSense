import React, { useState } from "react";

type ChatIputAreaProps = {
    value: string;
    onChange: (value: string) => void;
    onSend: () => void;
}

const ChatInputArea: React.FC<ChatIputAreaProps> = ({value, onChange, onSend}) => {
    const handleKeyDown =  (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key == "Enter") {
            onSend();
        }
    } 

    return (
        <footer className="chat-input-area-wrapper">
            <div className="chat-input-area">
                <input
                    className="chat-input-text-box"
                    type="text"
                    placeholder="Enter your question"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <button
                    className="chat-send-button"
                    onClick={onSend}
                    disabled={!value.trim()}
                >
                    Send
                </button>
            </div>
        </footer>
    )
}

export default ChatInputArea;