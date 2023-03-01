
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import {Tag} from '../_components/Tag';
import { accountService, alertService } from '@/_services';

function Update({ history }) {
    const user = accountService.userValue;
    const [profile, setProfile] = useState({})
    React.useEffect(() => {
        accountService.getUserProfile()
        .then((res) => {
            setProfile(res.data)
        })
        .catch(err => console.log(err + " " + err.response))
      }, {});

    
    const initialValues = {
        first_name: profile.first_name,
        last_name: profile.last_name,
        email: profile.email,
        old_password: '',
        new_password: '',
        confirm_new_password: ''
    };

    const validationSchema = Yup.object().shape({
        first_name: Yup.string().required('First name is required'),
        last_name: Yup.string().required('Last name is required'),
        email: Yup.string()
            .required('Email is required')
            .email('Email is invalid'),
        old_password: Yup.string(),
        new_password: Yup.string()
            .min(6, 'Password must be at least 6 characters'),
        confirm_new_password: Yup.string()
            .when('new_password', (new_password, schema) => {
                if (new_password) return schema.required('Confirm New Password is required');
            })
            .oneOf([Yup.ref('new_password')], 'Passwords must match')
    });

    function onSubmit(fields, { setStatus, setSubmitting }) {
        setStatus();
        accountService.update(user.data.id, fields)
            .then(() => {
                alertService.success('Update profile details successful. You may want to logout and login again to see the update', { keepAfterRouteChange: true });
                setSubmitting(false);
            })
            .catch(error => {
                setSubmitting(false);
                alertService.error(error + error.response);
            });
        
        if(fields.old_password && fields.new_password) {
            accountService.changePassword(fields)
            .then(() => {
                alertService.success('Password changed successful', { keepAfterRouteChange: true });
                history.push({ pathname: "/" });
            })
            .catch(error => {
                setSubmitting(false);
                alertService.error(error + " " + error.response.data.old_password + " " + error.response.data.new_password);
            });;
        }
        
    }
    const [isDisabled, setDisabled] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    function onDelete() {
        if (confirm('Are you sure you want to delete account?')) {
            setIsDeleting(true);
            accountService.delete(user.data.id)
                .then(() => alertService.success('Account deleted successfully'));
        }
    }

    function unit({user}) {
        if(user.type === "Tutor") {
            return ( <div className="form-group">
            <label>Unit</label>
            <Tag/>
        </div>);
        }
        else return 
    }

    return (
        <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
            {({ errors, touched, isSubmitting }) => (
                <Form onKeyDown={event => event.key === "Enter"? setDisabled(true):null} onKeyUp={event => event.key === "Enter"? setDisabled(false):null}>
                    <h1>Update Profile</h1>
                    <div className="form-row">
                        {/* <div className="form-group col">
                            <label>Type</label>
                            <Field name="type" as="select" className={'form-control' + (errors.type && touched.type ? ' is-invalid' : '')}>
                                <option value=""></option>
                                <option value="Tutor">Tutor</option>
                                <option value="Student">Student</option>
                            </Field>
                            <ErrorMessage name="type" component="div" className="invalid-feedback" />
                        </div> */}
                        <div className="form-group col-3">
                            <label>First Name</label>
                            <Field name="first_name" type="text" className={'form-control' + (errors.first_name && touched.first_name ? ' is-invalid' : '')} />
                            <ErrorMessage name="first_name" component="div" className="invalid-feedback" />
                        </div>
                        <div className="form-group col-3">
                            <label>Last Name</label>
                            <Field name="last_name" type="text" className={'form-control' + (errors.last_name && touched.last_name ? ' is-invalid' : '')} />
                            <ErrorMessage name="last_name" component="div" className="invalid-feedback" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <Field name="email" type="text" className={'form-control' + (errors.email && touched.email ? ' is-invalid' : '')} />
                        <ErrorMessage name="email" component="div" className="invalid-feedback" />
                    </div>
                    {unit({user})}
                    <h3 className="pt-3">Change Password</h3>
                    <p>Leave blank to keep the same password</p>
                    <div className="form-group">
                            <label>Old Password</label>
                            <Field name="old_password" type="password" className={'form-control' + (errors.old_password && touched.old_password ? ' is-invalid' : '')} />
                            <ErrorMessage name="old_password" component="div" className="invalid-feedback" />
                    </div>
                    <div className="form-row">
                        <div className="form-group col">
                            <label>New Password</label>
                            <Field name="new_password" type="password" className={'form-control' + (errors.new_password && touched.new_password ? ' is-invalid' : '')} />
                            <ErrorMessage name="new_password" component="div" className="invalid-feedback" />
                        </div>
                        <div className="form-group col">
                            <label>Confirm New Password</label>
                            <Field name="confirm_new_password" type="password" className={'form-control' + (errors.confirm_new_password && touched.confirm_new_password ? ' is-invalid' : '')} />
                            <ErrorMessage name="confirm_new_password" component="div" className="invalid-feedback" />
                        </div>
                    </div>
                    <div className="form-group">
                        <button type="submit" disabled={isDisabled||isSubmitting} className="btn btn-primary mr-2">
                            {isSubmitting && <span className="spinner-border spinner-border-sm mr-1"></span>}
                            Update
                        </button>
                        <button type="button" onClick={() => onDelete()} className="btn btn-danger" style={{ width: '175px' }} disabled={isDeleting}>
                            {isDeleting
                                ? <span className="spinner-border spinner-border-sm"></span>
                                : <span>Delete Account</span>
                            }
                        </button>
                        <Link to="." className="btn btn-link">Cancel</Link>
                    </div>
                </Form>
            )}
        </Formik>
        
    )
}

export { Update };
