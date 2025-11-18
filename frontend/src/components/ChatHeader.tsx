import React from "react";

type ChatHeaderProps = {
    title?: string;
    subtitle?: string;
    resetDisabled?: boolean;
    onReset: () => void;
};

const ChatHeader: React.FC<ChatHeaderProps> = ({
    title = "Autosense", 
    subtitle = "Your car assistant", 
    onReset, 
    resetDisabled = false}) => {
    
    return (
        <header className="chat-header">
            <div className="chat-header-texts">
                <h1 className="chat-header-title">{title}</h1>
                <p className="chat-header-subtitle">{subtitle}</p>
            </div>
            <button
                className="chat-reset-button"
                onClick={onReset}
                disabled={resetDisabled}
                >
                Start to new chat
            </button>
        </header>
    );
};

export default ChatHeader;