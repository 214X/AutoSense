import React from "react";

type ChatHeaderProps = {
    title?: string;
    subtitle?: string;
};

const ChatHeader: React.FC<ChatHeaderProps> = ({title = "Autosense", subtitle = "Your car assistant"}) => {
    return (
        <header className="chat-header">
            <div className="chat-header-texts">
                <h1 className="chat-header-title">{title}</h1>
                <p className="chat-header-subtitle">{subtitle}</p>
            </div>
        </header>
    );
};

export default ChatHeader;