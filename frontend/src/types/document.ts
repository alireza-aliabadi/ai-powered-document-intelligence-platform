export interface Document {

    id:string;

    name:string;

    status:
    | "processing"
    | "completed"
    | "failed";

}