import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js"; 
import {getDatabase,ref,push, onValue,remove} from "https://www.gstatic.com/firebasejs/9.15.0/firebase-database.js";
const appSitting={
    databaseURL:"https://ai-wave-421620-default-rtdb.firebaseio.com/"
}

const app=initializeApp(appSitting);
console.log(app)
const database=getDatabase(app);
const poeple=ref(database,"peoples");
const ul=document.getElementById("ul");
function transformObject(obj) {
    // Remove extra spaces from the values
    const name = obj.name.trim();
    const gender = obj.gender.trim();
    const socialSkill = obj.socialSkill.trim();
    const domain = obj.domain.trim();
    const score = obj.Score.trim();
  
    // Construct the transformed string
    const transformedString = `Name: ${name}    Gender: ${gender}    Social Skill: ${socialSkill}    Speciality: ${domain}    Score: ${score}`;
  
    return transformedString;
}
onValue(poeple,function(snapshot) {
    snapshot=Object.entries(snapshot.val());
    snapshot=Object.values(snapshot);
    for (let i = 0; i < snapshot.length; i++) {
        const element = snapshot[i][1];
        ul.innerHTML+=`<li>${transformObject(element)}<li>`
        
    }
    console.log(snapshot);
})