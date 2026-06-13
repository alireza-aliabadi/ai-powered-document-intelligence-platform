import {useState} from "react";
import {uploadDocument} from "../api/documents";


export default function UploadBox(){


const [file,setFile]=useState<File>();

const [message,setMessage]=useState("");



async function upload(){


    if(!file)
        return;


    setMessage(
        "Uploading..."
    );


    await uploadDocument(
        file
    );


    setMessage(
        "Uploaded. Processing..."
    );

}



return (

<div>

<h2>
Upload Document
</h2>


<input

type="file"

onChange={
e=>setFile(
    e.target.files?.[0]
)
}

/>


<button onClick={upload}>
Upload
</button>


<p>
{message}
</p>


</div>

)

}