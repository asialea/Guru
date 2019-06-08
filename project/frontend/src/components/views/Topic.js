import React, { Component } from 'react';
import {connect} from "react-redux";
import '../static/Home.css';
import Navbar from './Navbar';
import '../static/Forum.css';
import TextareaAutosize from 'react-textarea-autosize';
import {headers} from '../forms/global.js'
import Comments from './Comments';


class Topic extends Component{

    state = {
      posts:[],
      topic:"",
      meta:null,
      avi:null,
    }

    fetchPosts =()=>{
      headers["Authorization"] = `Token ${this.props.token}`;
      fetch(`/api/post/${this.props.match.params.topic_id}/`,{headers,method:"GET"})
        .then(response => { return response.json();}).then(responseData => {return responseData;})
        .then (json => {this.setState({posts: json.data}); this.setState({topic:json.topic});
        this.setState({meta:json.meta}); this.setState({avi:json.user_avi});})
        .catch(err => {console.log("fetch error" + err);
         });
    }

    newPost = (topic,category,text,reply_to,user_id)=>{
      let body = JSON.stringify({topic,category,text,reply_to,user_id});
      headers["Authorization"] = `Token ${this.props.token}`;
      return fetch(`/api/post/${this.props.match.params.topic_id}/`, {headers,body,method:"POST"})
        .then(res => {return res.json();}).then(()=>this.fetchPosts())
        .catch(err => {console.log("fetch error" + err)})
    }

    submitPost = (e) =>{
      e.preventDefault();
      this.newPost(this.props.match.params.topic_id,this.props.match.params.category_id,this.state.post,null,this.props.user.id)
    }

    componentWillMount(){
      this.fetchPosts()
    }

  render(){
    var avi = this.state.avi;
    return(
    <div id="topic">
      <header>
        <Navbar history={this.props.history}/>
      </header>
      <div className="flex-box">
        <div className="forum-body">
            <div id="post-list">
              <h1 className="forum-h1">{this.state.topic}</h1>
              <div className="post">
              <div className="post-avi" style = {avi ? {backgroundImage: `url(${avi})`} : {}}></div>
              <div className="text">
                <TextareaAutosize id="new-post" onChange={e => this.setState({post: e.target.value})} maxLength="500" minRows={1} maxRows={6}
                 placeholder="Create a post..."/>
                <button onClick={this.submitPost} className="post-submit">Post</button>
              </div>
              </div>
              <div>
              <Comments fetchPosts={this.fetchPosts} newPost={this.newPost} match={this.props.match}
              comments={this.state.posts} meta={this.state.meta} />
              </div>
            </div>

        </div>
      </div>
    </div>
    )
  }
}

const mapStateToProps = state => {
    return {
      user: state.auth.user,
      token:state.auth.token,
    }
}

export default connect(mapStateToProps)(Topic);
