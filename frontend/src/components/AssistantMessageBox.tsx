import React from "react";

type AssistantMessageBoxProps = {
    content: string;
}

const AssistantMessageBox: React.FC<AssistantMessageBoxProps> = ({content}) => {
    return (
        <div className="assistant-message-box">
            {content}
        </div>
    )
}

export default AssistantMessageBox;