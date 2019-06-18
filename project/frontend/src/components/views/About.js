import React, { Component } from 'react';
import {connect} from "react-redux";
import Navbar from './Navbar';
import '../static/About.css';
import Skills from '../forms/Skills'
import Interests from '../forms/Interests'
import Experience from '../forms/Experience'
import Education from '../forms/Education'
import AboutUser from '../forms/AboutUser'
import {FaUser,FaMapMarker,FaEdit} from 'react-icons/fa';
import IconButton from '@material-ui/core/IconButton';
import {Tabs,TabLink,TabContent} from 'react-tabs-redux';


class About extends Component{

  state = {
    aboutUser:{},
    form_hidden:true,
    avi:{},

  }

  parse_type(type){
    return (type ==='MR' ? 'Mentor' : 'Mentee')
  }

  show = (e) =>{
    this.setState({form_hidden:!this.state.form_hidden});
  }

  fetchAvi = ()=>{
    fetch(`/api/avi/${this.props.user.id}/`)
      .then(response => { return response.json();}).then(json =>this.setState({avi: json}))
      .catch(err => {console.log("fetch error" + err);});
            }

  fetchAboutUser = ()=>{
    fetch(`/api/aboutUser/${this.props.user.username}/`)
      .then(response => { return response.json();}).then(json =>this.setState({aboutUser: json}))
      .then(this.setState({hidden:true}))
      .catch(err => {console.log("fetch error" + err);})
  }

  componentWillMount(){
      this.fetchAboutUser();
      this.fetchAvi();

    }

  render(){
    return(
    <div className="body" id="about">
      <header>
        <Navbar history={this.props.history}/>
      </header>
      <div className="flex-box">
      <div className="about-header"></div>
      <div className="about-body">

        <section id="bio-section">
          <div className="square-container">
            <img id="pro-pic" alt="user avi" src={this.state.avi.avi_path}/>
          </div>
          <div id="bio-contact">
          <AboutUser  fetchAvi={this.fetchAvi} hidden={this.state.form_hidden} fetchAboutUser={this.fetchAboutUser} aboutUser={this.state.aboutUser}/>
          </div>
        </section>

        <section id="about-user">
          <p id="name">
            <IconButton onClick={this.show}><FaEdit  className="about-expand"/></IconButton>
          {this.props.user.first_name} {this.props.user.last_name}
          </p>
          <p><FaUser/> @{this.props.user.username}   ({this.parse_type(this.props.user.type)})</p>
          <p><FaMapMarker/> {this.state.aboutUser.location}</p>
        </section>

        <section id="resume">
          <Tabs>
          <div id="tablinks">
            <TabLink className={!this.state.hidden ? 'hidden':'tablink contact-tab'} to="tab5">About</TabLink>
            <TabLink className={!this.state.hidden ? 'hidden':'tablink'} to="tab1" default>Experience</TabLink>
            <TabLink className={!this.state.hidden ? 'hidden':'tablink'} to="tab2">Education</TabLink>
            <TabLink className={!this.state.hidden ? 'hidden':'tablink'} to="tab3">Skills </TabLink>
            <TabLink className={!this.state.hidden ? 'hidden':'tablink'} to="tab4">Interests</TabLink>
          </div>

          <TabContent className={!this.state.hidden ? 'hidden':'contact-tab'} for="tab5">
          <article>
          <AboutUser fetchAvi={this.fetchAvi} hidden={this.state.form_hidden} fetchAboutUser={this.fetchAboutUser} aboutUser={this.state.aboutUser}/>

          </article>
          </TabContent>

            <TabContent className={!this.state.hidden ? 'hidden':''} for="tab1">
            <article>
              <Experience/>
            </article>
            </TabContent>

            <TabContent className={!this.state.hidden ? 'hidden':''} for="tab2">
            <article>
              <Education/>
            </article>
            </TabContent>

            <TabContent className={!this.state.hidden ? 'hidden':''} for="tab3">
            <article>
              <Skills/>
            </article>
            </TabContent>

            <TabContent className={!this.state.hidden ? 'hidden':''} for="tab4">
            <article>
              <Interests/>
            </article>
            </TabContent>

          </Tabs>
  </section>
        </div>
      </div>
      <div>{this.props.children}</div>
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



export default connect(mapStateToProps)(About);
