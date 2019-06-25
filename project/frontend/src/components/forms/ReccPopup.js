import React from 'react';
import '../static/Home.css';
import {FaTimes} from 'react-icons/fa';
import IconButton from '@material-ui/core/IconButton';
import {connect} from "react-redux";
import {headers} from './global.js'

class ReccPopup extends React.Component {

  state:{
    text:null,
    rating:null,
  }

  addRec(text,author,user_id,rating){
      let body = JSON.stringify({text,author,user_id,rating});
      headers["Authorization"] = `Token ${this.props.token}`;
      fetch(`/api/rec/${this.props.username}/`, {body,headers,method:"POST"}).then(res => {return res.json();})
        .then(responseData => {return responseData;}).then(()=>this.props.fetch())
        .catch(err => {console.log("fetch error" + err)})
    }

  recSubmit(e){
    e.preventDefault();

    this.addRec(this.state.text,this.props.user.id,this.props.user_id,this.state.rating)

  }

  render() {
return (
  <div className='popup'>
    <div className='popup_inner'>
      <IconButton onClick={this.props.closePopup}><FaTimes/></IconButton>
      <p id="banner2">{this.props.text}  </p>
      <textarea onChange={e => this.setState({text:e.target.value})} maxLength="500" placeholder="Write a Reccomendation" required></textarea>
      <p>Leave a Rating :
        <select id="rating" onChange={e => this.setState({rating: parseInt(e.target.value)})}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
        </select>
      </p>
      <button onClick={(e)=>{ this.recSubmit(e); this.props.closePopup(e);}} className="submit">Submit</button>
    </div>
  </div>
    );
    }
  }
  const mapStateToProps = state => {
      return {
          user: state.auth.user,
          token: state.auth.token,
      }
  }



  export default connect(mapStateToProps)(ReccPopup);
