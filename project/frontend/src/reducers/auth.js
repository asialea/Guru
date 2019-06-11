const initialState = {
  token: localStorage.getItem("token"),
  isAuthenticated: null,
  isLoading: true,
  user: null,
  errors:{},
  login_errors:{}
};


export default function auth(state=initialState, action) {

  switch (action.type) {

    case 'USER_LOADING':
      return {...state, isLoading: true};

    case 'USER_LOADED':
      return {...state, isAuthenticated: true, isLoading: false, user: action.user};

    case 'REGISTRATION_SUCCESSFUL':
      localStorage.setItem("token", action.data.token);
      return {...state, ...action.data, isAuthenticated: true, isLoading: false, errors: null};

    case 'REGISTRATION_FAILED':
      return {...state, ...action.data, isAuthenticated: false, isLoading: false,
        errors: action.data};
    case 'LOGIN_SUCCESSFUL':
      localStorage.setItem("token", action.data.token);
      return {...state, ...action.data, isAuthenticated: true, isLoading: false,
        errors: null,login_errors:null};

    case 'AUTHENTICATION_ERROR':
    case 'LOGIN_FAILED':
      return {...state, ...action.data, isAuthenticated: false, isLoading: false,
        errors:null, login_errors: action.data};

    case 'UPDATE_SUCCESSFUL':
      return {...state, user: action.user, isAuthenticated: true, isLoading: false,
        errors:null};

    case 'UPDATE_FAILED':
      return {...state, isAuthenticated: true, isLoading: false,
        errors: action.data};

    case 'LOGOUT_SUCCESSFUL':
      localStorage.removeItem("token");
      return {...state, errors: action.data, token: null, user: null,
        isAuthenticated: false, isLoading: false};

    default:
      return state;
  }
}
