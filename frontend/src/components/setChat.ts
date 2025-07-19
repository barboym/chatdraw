
import {ref} from 'vue';


export type SystemMessage = {
  text?:string
  imageUrl?:string
  isSketch:boolean
  isUser:boolean
}

type Message = {
  mtype:string
  content:string
}
type Response = {
  response:Message[]
  next_context:string
}

export function setChat(context_start:string=''){
    if (context_start == ''){
      context_start='greeting_start'
    }
    const messages = ref<SystemMessage[]>([]);
    const context = ref(context_start);
    const waitingForResponse = ref(false)


    async function sendMessage(message:Message){
        waitingForResponse.value=true
        addMessages([message],true)
        await fetch('http://127.0.0.1:8005/', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            context: context.value,
        })
        })
        .then(response => response.json())
        .then(getContext)
        .then((x)=>addMessages(x,false))
        .catch(error => console.error('Error:', error))
        .finally(messageTrigger);
    }

    function getContext(responseJson:Response) {
        context.value = responseJson.next_context;
        return responseJson.response;
    }

    function addMessages(responseArray:Message[],isUser:boolean) {
        for (const obj of responseArray) {
            if (obj.mtype === "text") {
                messages.value.push({"text":obj.content,"isSketch":false,"isUser":isUser});
            } else if (obj.mtype === "image") {
                messages.value.push({"imageUrl":`data:image/png;base64,${obj.content}`,"isSketch":true,"isUser":isUser});
            } else {
                throw new Error("Invalid mtype: must be either 'text' or 'image'");
            }
        }
    }

    function messageTrigger() {
        waitingForResponse.value=false
    }
    return {messages, waitingForResponse, sendMessage}
}


// const {messages, waitingForResponse, sendMessage} = setChat("greeting_start.DrawingProject_chooseconcept")
// await sendMessage({"mtype":"text","content":"monkey"})
// console.log(messages.value)

