import React,{Component} from "react";
import { View,Text } from "react-native";
import { Camera } from "expo";
import $ from "jquery";
import { CFactory } from "react";



export default class App extends Component{


  constructor(props){
    super(props);
    this.send=this.send.bind(this);
  }

  render(){
    return(

      <View style={{flex:1}}>
        <Text>hello world</Text>
      </View>
    )
  }

  capture(){
    return "photo data"
  }

  componentDidMount(){
  

    //set interval to capture  and send photo every 1 second
  }
  componentWillMount(){
    //ask permissions
    //send hello to server
    this.send({message:"hello"})
  }

  send(data){
    //sends messages to server
    
    fetch("http://192.168.43.118:8000/read/",{
      method:"POST",
      headers:{

      },
      credentials:"same-origin",
      body:JSON.stringify(data)
    }).then(data=>{
      alert(data._bodyText)
    })  
  }
}