// Browser ESM client for Supabase
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const supabaseUrl = 'https://rdzmlzrsvmewwizimgnb.supabase.co';
const supabaseKey = 'sb_publishable_rD3RjsKnJAtMOlGggsFr9g_rK9RitvU'; // anon/public key

export const supabase = createClient(supabaseUrl, supabaseKey);

export async function supabaseSignUp(email, password, profile) {
    const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: { data: profile || {} }
    });
    if (error) throw error;
    return data;
}

export async function supabaseSignIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data;
}
