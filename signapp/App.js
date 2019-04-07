import React from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import Camera from 'expo';
import $ from 'jquery';
import Speech from 'react-native'
export default class App extends React.Component {

  constructor(){
    this.camera=null;
    this.state={
      ip_address:"192.168.56.1",
      orientation:Camera.Front,
    }
  }
  async capture(){
    var photo=camera.takePictureAsync();
    $.ajax({
      method:"post",
      data:{
        hand_roi:photo.base64
      },
      url:this.state.ip_address+"/read/",
      success:function (data) {
        speech.speak(data);
      }
    })
    setInterval(this.capture,1000)
  }
  async componentDidMount(){
     setInterval(this.capture,0)
  }
  render() {
    return (
      <View style={styles.container}>
        <Camera ref={(ref)={
          this.camera=camera;
        }}/>
        <TextInput
        onPress={()=>{
          this.setState()
        }}
        placeholder="enter ip address"
        />
      <Button
      onPress={()=>{
        this.setState({
          orientation:Camera.Back
        })
      }}>Flip camera</Butoon>
      </View>
    );
  }
}



const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
