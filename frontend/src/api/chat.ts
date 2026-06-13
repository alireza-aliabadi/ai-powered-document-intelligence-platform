import api from "./client";


export async function askQuestion(
    question:string
){

    const response =
        await api.post(
            "/documents/chat/",
            {
                question
            }
        );


    return response.data;

}
