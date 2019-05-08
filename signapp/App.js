import React from 'react';
import { Text, TextInput,Button,View, TouchableOpacity,StyleSheet } from 'react-native';
import { Camera, Permissions, LinearGradient,ImageManipulator } from 'expo';
import { Icon } from 'native-base';
import GestureRecognizer, {swipeDirections} from 'react-native-swipe-gestures';

export default class App extends React.Component {
  constructor(props){
    
    super(props);
    this.camera=null;
    this.state = {
      hasCameraPermission: null,
      type: Camera.Constants.Type.back,
      showSettings: true,
      word:""
    };
    this.options={
      skipProcessing: true,
      base64:true
    }
  }
  
  snap = async () => {
    if (this.camera) {
      //console.log(this.camera.getAvailablePictureSizesAsync())
      let photo = await this.camera.takePictureAsync(this.options);
      const resized_image=await ImageManipulator.manipulateAsync(photo.uri,[{ resize: { width: 400, height: 400 } }],{ format: 'jpg',base64:true })
      console.log(resized_image.uri)

      let formData = new FormData();
      formData.append('hand_roi', { uri: resized_image.uri, name: 'photo', type:'jpg' });
      console.log(formData)
      /*
     fetch("http://10.42.0.1:8000/read/",{
      method:"POST",
      headers: {'Content-Type':'application/x-www-form-urlencoded'}, // this line is important, if this content-type is not set it wont work
      body: 'hand_roi='+resized_image.base64,
      credentials:"same-origin",
    })
    .then((res) => {return res.text();})
    .then((data) => { console.log(data); this.setState({word:data})});
    */

    }
  };

  async componentWillMount(){
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }
  async componentDidMount() {
    setInterval(this.snap,5000)
  }

  onSwipeUp(gestureState) {
    this.setState({ showSettings: true });
  }

  onSwipeDown(gestureState) {
    this.setState({ showSettings: false });
  }

  render() {
    const config = {
      velocityThreshold: 0.3,
      directionalOffsetThreshold: 80
    };
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else {
      return (
          <Camera 
          style={{ flex: 1 }} 
          type={this.state.type} 
          ref={ref => { this.camera = ref; }}
          >
          <GestureRecognizer
              onSwipeUp={state => this.onSwipeUp(state)}
              onSwipeDown={state => this.onSwipeDown(state)}
              config={config}
              style={{
                flex: 1,
                backgroundColor: "transparent"
              }}
            >
            {this.state.showSettings ?(
            <LinearGradient
              colors={['#0069d900', '#0069d9', '#0069d900']}
              style={{
                flex: 1,
                backgroundColor: '#000000a0',
                flexDirection: 'row',
                justifyContent: 'space-between',
                alignItems:'center',
                paddingLeft:'8%',
                paddingRight:'8%'
              }}>
              <View>
                <TextInput  placeholder="Enter address..."
                            multiline={true} 
                            style={{
                              fontSize:30,
                              width:250,
                              color:'#ffffff',
                              backgroundColor:'#ffffff05'
                              }} />              
              </View>
              <View>
                <Icon 
                name='swap' 
                onPress={() => {
                  this.setState({
                    type: this.state.type === Camera.Constants.Type.back
                      ? Camera.Constants.Type.front
                      : Camera.Constants.Type.back,
                  });
                }}
                style={{color:"#ffffff",paddingRight:20,fontSize:30}}
                 />
                </View>
            </LinearGradient>):null}
            </GestureRecognizer>
          </Camera>
      );
    }
  }
}


