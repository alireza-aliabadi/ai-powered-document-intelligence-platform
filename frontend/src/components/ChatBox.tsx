import {useState} from "react";
import {askQuestion} from "../api/chat";


export default function ChatBox(){


const [question,setQuestion]
=useState("");

const [answer,setAnswer]
=useState("");



async function send(){


const result =
 await askQuestion(
    question
 );


setAnswer(
 result.answer
);


}



return (

<div>


<h2>
Document Chat
</h2>


<textarea

value={question}

onChange={
e=>setQuestion(
e.target.value
)
}

/>


<button onClick={send}>
Ask
</button>



<div>

<h3>
Answer
</h3>

<p>
{answer}
</p>


</div>


</div>

)

}