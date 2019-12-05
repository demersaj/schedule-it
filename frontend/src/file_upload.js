import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import Moment from 'react-moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

#source: https://programmingwithmosh.com/javascript/react-file-upload-proper-server-side-nodejs-easy/
#Allows for a single file to be uploaded to a reservation
 <input type="file" name="file" onChange={this.onChangeHandler}/>

onChangeHandler=event=>{

#stores the files uploaded
    console.log(event.target.files[0])

}

constructor(props) {
    super(props);
    
    #file is originally null
      this.state = {
        selectedFile: null
      }
   
  }
  
  #passes file
  onChangeHandler=event=>{
    this.setState({
      selectedFile: event.target.files[0],
      loaded: 0,
    })
  }
  
  #buttom to upload the file
  <button type="button" class="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button>
  
  #POST request
  axios.post(path.File, data, {
      })
      .then(res => { // then print response status
        console.log(res.statusText)
      })
      
      #uploads file
      onClickHandler = () => {
   const data = new FormData()
   data.append('file', this.state.selectedFile)
   axios.post(path.File, data, { 
  })
.then(res => { // then print response status
    console.log(res.statusText)
 })
}
