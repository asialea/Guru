import React, { Component } from 'react';
import {connect} from "react-redux";
import {auth} from "../../actions";
import '../static/Home.css';


class Register extends Component {

  state = {
    username: "",
    email:"",
    first_name:"",
    last_name:"",
    password: "",
    type:"ME",
  }

  registerSubmit = e => {
    e.preventDefault();
    if(this.state.password === document.getElementById("confirm_pass").value){
          this.props.register(this.state.username,this.state.email,this.state.first_name,
          this.state.last_name,this.state.password,this.state.type,this.state.username);
    }else{
       alert("Password does not match");
     }
  }

  render () {
      return (
    <div className="form-container">
        <form onSubmit={this.registerSubmit}>
        <p id = "banner"> Join the tech community </p>
        <p id = "banner2"> Get started - it's free </p>
          <div className="row">
            <div className="col-6">
              <input className="inputdiv"  type="text" placeholder="First Name" maxLength="30" pattern="^[a-zA-Z]+$"
              onChange={e => this.setState({first_name: e.target.value})} required />
            </div>
            <div className="inputdiv col-6">
              <input className="" type="text" placeholder="Last Name" maxLength="150" pattern="^[a-zA-Z]+$"
              onChange={e => this.setState({last_name: e.target.value})} required/>
            </div>

            <div className="inputdiv col-12">
              <input className = ""  type="text" placeholder="Username" maxLength="30" pattern="^[a-zA-Z0-9]+$"
              onChange={e => this.setState({username: e.target.value})} required/>
            </div>

            <div className="inputdiv col-12">
              <input className = ""  type="email" placeholder="Email"  maxLength="254"
              onChange={e => this.setState({email: e.target.value})} required/>
            </div>

            <div className="inputdiv col-12">
              <input className = ""  type="password" placeholder="Password" maxLength="128"
              onChange={e => this.setState({password: e.target.value})} required/>
            </div>

            <div className="inputdiv col-12">
              <input id="confirm_pass"  type="password" placeholder="Confirm Password" required/>
            </div>


            <div className="inputdiv col-12">
              <select className="" placeholder="Account Type"  onChange={e => this.setState({type: e.target.value})}>
                <option value="ME">Mentee</option>
                <option value="MR">Mentor</option>
              </select>
            </div>


            <div className="inputdiv col-12">
              <button className = "submit" >Sign Up</button>
            </div>
         </div>
             {this.props.errors.length > 0 && (
               <ul>
                 {this.props.errors.map(error => (
                   <li key={error.field}>{error.message}</li>
                 ))}
               </ul>
             )}
        </form>
      </div>

      );
   }
}

const mapStateToProps = state => {
  let errors = [];
  if (state.auth.errors) {
    errors = Object.keys(state.auth.errors).map(field => {
      return {field, message: state.auth.errors[field]};
    });
  }
  return {
    errors,
    isAuthenticated: state.auth.isAuthenticated
  };
}

const mapDispatchToProps = dispatch => {
  return {
    register: (username,email,first_name,last_name,password,type) =>
    dispatch(auth.register(username,email,first_name,last_name,password,type)),
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Register);
