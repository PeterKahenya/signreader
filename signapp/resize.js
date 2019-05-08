import { ImageManipulator } from 'expo';
import React from 'react-native'

export default class Resize extends React.Component{

constructor(props){
super(props)
this.state={

}
this.resize=this.resize.bind(this);
}


resize(photo){

const resized_image=ImageManipulator.manipulateAsync(photo.uri, [{ resize: { width: 640, height: 480 } }],{ format: 'jpg' })
return resized_image.uri;

}


render(){




}




}
