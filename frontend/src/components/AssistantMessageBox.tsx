import React from "react";
import ReactMarkdown from "react-markdown";

type AssistantMessageBoxProps = {
    content: string;
}

const AssistantMessageBox: React.FC<AssistantMessageBoxProps> = ({content}) => {
    return (
        <div className="assistant-message-box">
            <ReactMarkdown>
                {content}
            </ReactMarkdown>
        </div>
    )
}

export default AssistantMessageBox;