import React from "react";

type UserMessageBoxProps = {
    content: String;
}

const UserMessageBox: React.FC<UserMessageBoxProps> = ({content}) => {
    return (
        <div className="user-message-box">
            {content}
        </div>
    )
}

export default UserMessageBox;