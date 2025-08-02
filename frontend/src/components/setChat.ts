
import {ref} from 'vue';


export type SystemMessage = {
  text?:string
  imageUrl?:string
  isSketch:boolean
  isUser:boolean
}

type Message = {
  mtype:"text" | "image" // 'image' means svg string
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
        if (waitingForResponse.value === true) return
        waitingForResponse.value=true
        addMessagesSend(message)
        await fetch('/', {
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
        .then(stripAndSetContext)
        .then((msgs)=>addMessages(msgs))
        .catch(error => console.error('Error:', error))
        .finally(() => {waitingForResponse.value=false})
    }

    function stripAndSetContext(responseJson:Response) {
        context.value = responseJson.next_context;
        return responseJson.response;
    }

    function addMessages(responseArray:Message[]) {
        for (const msg of responseArray) {
            if (msg.mtype === "text") {
                messages.value.push({"text":msg.content,"isSketch":false,"isUser":false});
            } else if (msg.mtype === "image") {
                messages.value.push({"imageUrl":`data:image/png;base64,${msg.content}`,"isSketch":true,"isUser":false});
            } else {
                throw new Error("Invalid mtype: must be either 'text' or 'image'");
            }
        }
    }

    function addMessagesSend(msg:Message) {
      if (msg.mtype === "text") {
          messages.value.push({"text":msg.content,"isSketch":false,"isUser":true});
      } else if (msg.mtype === "image") {
          console.log("sending svg:",msg.content)
          const blob = new Blob([msg.content], {type: 'image/svg+xml'});
          const url = URL.createObjectURL(blob);
          messages.value.push({"imageUrl":url,"isSketch":true,"isUser":true});
      } else {
          throw new Error("Invalid mtype: must be either 'text' or 'image'");
      }
    }

    return {messages, sendMessage}
}


// const {messages, sendMessage} = setChat("greeting_start.DrawingProject_chooseconcept")
// await sendMessage({"mtype":"text","content":"monkey"})
// console.log(messages.value)

