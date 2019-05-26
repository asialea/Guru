import React, { Component } from 'react';
import {connect} from "react-redux";
import {FaTimes,FaPlus} from 'react-icons/fa';
import {headers,findAndRemove} from './global.js'

class Education extends Component{
  state ={
    school:"",
    degree:"",
    location:"",
    start:"",
    end:null,

    new_edu:null,
    education:[],
    hidden:true,
  }
  show = (e) =>{
    this.setState({hidden:!this.state.hidden})
  }

  new_eduSubmit(e){
    e.preventDefault();
    var edu = {"user_id":this.props.user.id,"start":this.state.start,"end":this.state.end,"school":this.state.school,
    "location":this.state.location,"degree":this.state.degree};
    this.setState({new_edu:edu},()=>this.addEducation(this.state.new_edu));
    this.refs.location.value =""; this.refs.start.value ="";
    this.refs.school.value =""; this.refs.end.value ="";
    this.refs.degree.value ="";
      }

  addEdu_cb = () =>{
    var newArray = this.state.education;
    var edu = {"user_id":this.props.user.id,"start":this.state.start,"end":this.state.end,"school":this.state.school,
    "location":this.state.location,"degree":this.state.degree};
    newArray.push(edu);
    this.setState({education:newArray});
  }

  addEducation(edu){
    let body = JSON.stringify(edu);
    headers["Authorization"] = `Token ${this.props.token}`;
    fetch(`api/education/`,{headers,body,method:"POST",}).then(res => {return res.json();})
    .then(this.addEdu_cb)
    .catch(err => {console.log("fetch error" + err)});
  }

  deleteEdu_cb =(id)=>{
    var newArray = this.state.education;
    findAndRemove(newArray,'id',id);
    this.setState({education:newArray});
    }


  deleteEducation = (id) =>{
       let body = JSON.stringify({id});
       headers["Authorization"] = `Token ${this.props.token}`;
       fetch(`api/education/${id}/`, {headers,body,method:"DELETE"}).then(res => {return res.json();})
       .then(this.deleteEdu_cb(id))
       .catch(err => {console.log("fetch error" + err)})
      }

  fetchEducation(){
    fetch(`/api/user-edu/${this.props.user.username}/`).then(response => response.json())
      .then(json =>{this.setState({education: json});})
      .catch(err => {console.log("fetch error" + err);});
                  }

  componentWillMount(){
    this.fetchEducation();
  }

  render(){
      return(
      <div>
      <button onClick={this.show} className="accordion btn-animated"><h2>Education<FaPlus onClick={this.show} className="expand"/></h2></button>
      <div className={this.state.hidden ? 'hidden':'form'}>
       <div className="form-group">
        <input className="input-small group-1" ref="school" onChange={e => this.setState({school: e.target.value})} placeholder="School" type="text" required/>
        <input className="input-small group-1" ref="degree" onChange={e => this.setState({degree: e.target.value})} placeholder="Degree" type="text" required/>
        <input className="input-small group-1" ref="location" onChange={e => this.setState({location: e.target.value})} placeholder="Location" type="text" required/>
        <input className="input-small group-2" ref="start" onChange={e => this.setState({start: e.target.value})} id="start" type="date"/>
        <label>to</label>
        <input className="input-small group-2" ref="end" onChange={e => this.setState({end: e.target.value})} id="end" type="date"/>
       </div>
       <div className="form-group">
         <button className = "submit"  onClick={this.new_eduSubmit.bind(this)}>Submit</button>
       </div>
      </div>

        <div>
          {this.state.education.map((el,idx) => {
                return <div className="edu-ex" key={el.id}>
                     <h3 className="main res-item">{el.school}, </h3><span className="res-item">{el.location} -</span>
                     <span className="position">{el.degree} </span>
                      <FaTimes className={this.state.hidden ? 'hidden':'deleteSkill'} onClick={(e) => {this.deleteEducation(el.id);}}/>
                     <p className="edu res-item">{el.start} to {el.end}</p>
                </div>
            })}
        </div>
    </div>
      );
  }
}

const mapStateToProps = state => {
    return {
      token:state.auth.token,
        user: state.auth.user,
    }
}



export default connect(mapStateToProps)(Education);
